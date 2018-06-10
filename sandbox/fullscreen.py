from vispy import app, gloo, visuals, scene
app.use_app('pyqt5')

canvas = scene.SceneCanvas(keys='interactive', size=(600,600), show=True, fullscreen=True, bgcolor='red')
grid = canvas.central_widget.add_grid()
plot_view = grid.add_view(row=0, col=0, border_color='white')
plot_view.camera = 'panzoom'

if __name__ == '__main__':
    app.run()