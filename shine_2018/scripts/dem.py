"""
Hack at computing DEM in a nice way
Move this somewhere else!
"""
import os

import numpy as np
import matplotlib.colors
import astropy.units as u
import hissw

from synthesizAR.maps import EMCube

__all__ = ['GenericModel', 'IDLModel', 'HannahKontarModel']


class GenericModel(object):
    
    @u.quantity_input
    def __init__(self, maps, temperature: u.K, responses, **kwargs):
        self.temperature = temperature
        wvl = u.Quantity([m.meta['wavelnth']*u.Unit(m.meta['waveunit']) for m in maps])
        self.maps = [maps[i] for i in np.argsort(wvl)]
        self.response = [responses[i] for i in np.argsort(wvl)]
        self.wavelength = np.sort(wvl)
        
    def fit(self,):
        pass


class IDLModel(GenericModel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'dem_path' not in kwargs:
            raise ValueError('Must specify path to DEM IDL code')
        self.ssw = hissw.ScriptMaker(ssw_packages=self.ssw_packages, ssw_paths=self.ssw_paths,
                                     extra_paths=[kwargs.get('dem_path')])
        self.mapcube = np.stack([m.data for m in self.maps], axis=2)
        self.response_matrix = np.stack(self.response)
        
    def _fit(self, **kwargs):
        input_args = self.input_args
        input_args.update(kwargs)
        return self.ssw.run(self._template, args=input_args, save_vars=self.save_vars,
                            verbose=True,)
    
    def to_emcube(self, em):
        header = self.maps[0].meta.copy()
        del header['telescop']
        del header['detector']
        del header['waveunit']
        del header['instrume']
        del header['wavelnth']
        return EMCube(em, header, self.temperature,
                      plot_settings={'cmap': 'magma',
                                     'norm': matplotlib.colors.SymLogNorm(1, vmin=1e25, vmax=1e30)})


class HannahKontarModel(IDLModel):

    @property
    def ssw_packages(self,):
        return ['sdo/aia']

    @property
    def ssw_paths(self,):
        return ['aia', 'xrt']

    @property
    def input_args(self,):
        return {
            'log_temperature': np.log10(((self.temperature[1:]
                                          + self.temperature[:-1])/2.).to(u.K).value).tolist(),
            'temperature_bin_edges': self.temperature.to(u.K).value.tolist(),
            'saturation_level': 2e4,
            'edge_trim': 10,
            'aia_error_table_filename': os.path.join(self.ssw.ssw_home,
                                                     'sdo/aia/response/aia_V2_error_table.txt'),
            'n_sample': 1,
            'maps': self.mapcube.T.tolist(),
            'response_matrix': self.response_matrix.tolist(),
        }

    @property
    def save_vars(self,):
        return ['dem', 'dem_errors', 'logt_errors', 'chi_squared', 'dn_regularized']

    def fit(self, **kwargs):
        self.results = self._fit(**kwargs)
        em = np.transpose(self.results['dem'], axes=(2, 1, 0))/(u.cm**5)/u.K
        em = em*np.diff(self.temperature)
        return self.to_emcube(em)

    @property
    def _template(self,):
        return """
        data = {{maps}}
        print,size(data)
        ; Set some basic parameters
        nx=n_elements(data[*,0,0])
        ny=n_elements(data[0,*,0])
        nchannels=n_elements(data[0,0,*])

        ; Filter out bad pixels
        sat_lvl={{ saturation_level }}
        id=where(data ge sat_lvl,nid)
        if (nid gt 1) then data[id]=0.0
        id=where(data le 0,nid)
        if (nid gt 1) then data[id]=0.0
        edg0={{edge_trim}}
        data[0:edg0-1,*,*]=0.0
        data[*,0:edg0-1,*]=0.0
        data[nx-edg0:nx-1,*,*]=0.0
        data[*,ny-edg0:ny-1,*]=0.0

        ; Calculate errors
        data_errors=fltarr(nx,ny,nchannels)
        channels = [94,131,171,193,211,335]
        common aia_bp_error_common,common_errtable
        common_errtable=aia_bp_read_error_table('{{ aia_error_table_filename }}')
        for i=0,nchannels-1 do data_errors[*,*,i]=aia_bp_estimate_error(reform(data[*,*,i]),replicate(channels[i],nx,ny),n_sample={{ n_sample }})

        ; Get temperature bins
        response_logt = {{log_temperature}}
        temperature = {{temperature_bin_edges}}

        ; Calculate response functions
        response_matrix = {{ response_matrix }}

        ; DEM Calculation
        dn2dem_pos_nb,data,data_errors,response_matrix,response_logt,temperature,dem,dem_errors,logt_errors,chi_squared,dn_regularized"""