import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle


class HSClusterAnalysis:
    
    def __init__(self, spectral_data, class_masks:dict,):
        
        # Initialise Data
        self.spectral_data = spectral_data.copy()
        self.spectral_img = spectral_data.mean(axis=2).T
        self.img_h, self.img_w = self.spectral_img.shape
        self.class_masks = class_masks

        if len(self.class_masks) > 8:
            raise ValueError("<8 masks should be provided.")
        
        # Initialise Figure parameters
        plt.rcParams['figure.figsize'] = (13.5,12)
        self.clsfig = plt.figure(constrained_layout=True)
        spec = gridspec.GridSpec(ncols=4, nrows=6, figure=self.clsfig)
        
        self.f_ax0 = self.clsfig.add_subplot(spec[0, :]) # Image Tile
        self.f_ax0c = self.clsfig.add_subplot(spec[1, :]) # Image Class Tile

        self.f_ax10 = self.clsfig.add_subplot(spec[2, 0]) # Individual Algo slice plots
        self.f_ax11 = self.clsfig.add_subplot(spec[2, 1]) # Individual Algo slice plots
        self.f_ax12 = self.clsfig.add_subplot(spec[2, 2]) # Individual Algo slice plots
        self.f_ax13 = self.clsfig.add_subplot(spec[2, 3]) # Individual Algo slice plots
        
        self.f_ax20 = self.clsfig.add_subplot(spec[3, 0]) # Individual Algo slice plots
        self.f_ax21 = self.clsfig.add_subplot(spec[3, 1]) # Individual Algo slice plots
        self.f_ax22 = self.clsfig.add_subplot(spec[3, 2]) # Individual Algo slice plots
        self.f_ax23 = self.clsfig.add_subplot(spec[3, 3]) # Individual Algo slice plots

        self.f_ax3 = self.clsfig.add_subplot(spec[-2:, :]) # Analysis plot

        self.sq_axes = [self.f_ax10,  self.f_ax11, self.f_ax12, self.f_ax13,
                        self.f_ax20, self.f_ax21, self.f_ax22, self.f_ax23]
        self.axes_mapping = {k.upper():v for k,v in zip(class_masks.keys(), self.sq_axes)}

        # Set titles
        for eachtitle,eachax in self.axes_mapping.items():
            eachax.set_title(eachtitle.upper(), fontsize=10)
            
        
        self.prev_line_x, self.prev_line_y, self.specplt = [],[],None
        self.retain_dict = {}
        
        # Prepare the masks images for each of the models
        self.f_ax0.imshow(self.spectral_img,cmap='gray')
        self.hoverpatch = Rectangle((0,0), self.img_h, self.img_h, alpha=0.5)
        self.f_ax0.add_artist(self.hoverpatch)
        
        # Connect the event handlers to the plot
        self.clsfig.canvas.mpl_connect('button_press_event', self.click_axes)
        self.clsfig.canvas.mpl_connect('motion_notify_event', self.hover_axes)

        plt.show()
        plt.ion()
    
    def click_axes(self, event):
        x_pixel, y_pixel = int(event.xdata), int(event.ydata)

        if event.inaxes == self.f_ax0:
            ax=event.inaxes
            if self.hoverpatch != None:
                self.hoverpatch.remove()
                
            if int(x_pixel)>self.img_h/2 and int(x_pixel)<self.img_w - self.img_h/2:
                hvr_x = int(x_pixel)-self.img_h/2
            elif int(x_pixel)<=self.img_h/2:
                hvr_x = 0
            elif int(x_pixel)>=self.img_w - self.img_h:
                hvr_x = self.img_w - self.img_h
    
            self.hoverpatch = Rectangle((hvr_x,0), self.img_h, self.img_h, alpha=0.5)
            self.f_ax0.add_artist(self.hoverpatch)
            
            self.x_slc1 = int(hvr_x)
            self.x_slc2 = int(hvr_x+self.img_h)

            for modelname, modelmask in self.class_masks.items():
                _name = modelname.upper()
                if len(modelmask) > 0:
                    ax=self.axes_mapping[_name]
                    if ax.images != []:
                        for eachImg in ax.images:
                            eachImg.remove()
                    _data = modelmask.T[:,self.x_slc1:self.x_slc2].copy()
                    ax.imshow(_data,cmap='prism')
    
    def hover_axes(self, event):
        x_pixel, y_pixel = int(event.xdata), int(event.ydata)

        if event.inaxes in list(self.axes_mapping.values()):
            ax=event.inaxes
            if ax.images != []:
                for eachl in self.prev_line_x:
                    eachl.remove()
                for eachl in self.prev_line_y:
                    eachl.remove()

                self.prev_line_x = []
                self.prev_line_y = []

                if self.specplt != None:
                    self.specplt[0].remove()

                for emt,emx in self.axes_mapping.items():
                    if emx.images != []:
                        temp=emx.vlines(x_pixel,0,self.img_h-2,color='k',linewidth=1.5,linestyle='-.')
                        self.prev_line_x.append(temp)
                        temp=emx.hlines(y_pixel,0,self.img_h-2,color='k',linewidth=1.5,linestyle='-.')
                        self.prev_line_y.append(temp)

                spectral_data = self.spectral_data[self.x_slc1+x_pixel,y_pixel,:]
                self.specplt = self.f_ax3.plot(spectral_data)
                _title=''
                for k,v in self.axes_mapping.items():
                    if v == ax: 
                        _title = k
                        # Update the f_ax0 with similar class
                        if len(self.f_ax0c.images)==2:
                            self.f_ax0c.images[-1].remove()
                        _hover_class = self.class_masks[_title.lower()][self.x_slc1+x_pixel,y_pixel]
                        single_class_mask = self.class_masks[_title.lower()]==_hover_class
                        self.f_ax0c.imshow(single_class_mask.T, cmap='gray', alpha=1)
                self.f_ax3.set_title(_title, fontsize=12)



class SpectralAnalysis:
    def __init__(self, spectral_data):
        self.specfig, self.specaxes = plt.subplots(nrows=3,ncols=1,
                                                    gridspec_kw={'height_ratios': [1, 2, 2]},
                                                    figsize=(13,11))
        plt.tight_layout()
        self.spectral_data = spectral_data.copy()
        self.spectral_img = spectral_data.mean(axis=2).T
        self.img_h, self.img_w = self.spectral_img.shape
        
        self.prev_line_x, self.prev_line_y, self.specplt = None, None, None
        self.retain_dict = {}
        
        # Connect the event handlers to the plot
        self.specfig.canvas.mpl_connect('motion_notify_event', self.enter_axes)
        self.specfig.canvas.mpl_connect('button_press_event', self.mouse_clicked)
        
        # Plot the HSI image
        self.specaxes[0].imshow(self.spectral_img, cmap='gray', aspect='auto')
        
        # Set labels for the 
        self.specaxes[1].set_xlabel(r'$\lambda\ Band No.\longrightarrow$',fontsize=10)
        self.specaxes[1].set_ylabel(r'$Irradiance$',fontsize=10)

        # Set the y limits for the last two plots
        self.specaxes[1].set_ylim(0,self.spectral_data.max())
        self.specaxes[2].set_ylim(0,self.spectral_data.max())
        self.specaxes[1].grid()
        self.specaxes[2].grid()

        plt.show()
        plt.ion()

    def enter_axes(self, event):
        if event.inaxes == self.specaxes[0]:
            ax=event.inaxes
            if self.prev_line_x != None:
                self.prev_line_x.remove()

            if self.prev_line_y != None:
                self.prev_line_y.remove()
                
            if self.specplt != None:
                self.specplt[0].remove()

            x_pixel, y_pixel = int(event.xdata), int(event.ydata)
            
            self.prev_line_x=ax.vlines(x_pixel,0,self.img_h-2,color='r',linewidth=1,linestyle=':')
            self.prev_line_y=ax.hlines(y_pixel,0,self.img_w-2,color='r',linewidth=1,linestyle=':')
            
            spectral_data = self.spectral_data[x_pixel,y_pixel,:]
            self.specplt = self.specaxes[1].plot(spectral_data)
    
    def mouse_clicked(self,event):
        if event.inaxes==self.specaxes[0]:

            x_pixel, y_pixel = int(event.xdata), int(event.ydata)
            spectral_data = self.spectral_data[x_pixel,y_pixel,:]
    
            self.retain_dict[f'Pixel_({x_pixel},{y_pixel})'] = spectral_data
            try:
                self.specaxes[2].get_legend().remove()
                for each in self.specaxes[2].lines:
                    each.remove()
            except:
                pass
        
            for k,v in self.retain_dict.items():
                self.specaxes[2].plot(v, label=k)
                self.specaxes[2].legend()
    
