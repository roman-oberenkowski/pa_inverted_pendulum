import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput
from bokeh.plotting import figure, show, output_file
#data from simulation
from Simulation import FullSimulator

class InvertedPendulumVisualization:
    def __init__(self):
        # Set up data
        self.x_range=[-15, 15]
        self.y_range=self.x_range
        self.default_pendulum_length=0.6

        self.time_results, self.position_results, self.angle_results = ([], [], [])
        self.pendulum_length=self.default_pendulum_length
        self.frame=0
        #CDS--------------------------------------
        self.ip_temp_dict = dict(base_x=[0], base_y=[0], base_h=[5], base_w=[0.3], ball_x=[0], ball_y=[-5], ball_size=[10])
        self.ip_animation_data = ColumnDataSource(data=self.ip_temp_dict)
        self.line_temp_dict = dict(line_xs=[0, 0], line_ys=[0, -5])
        self.line_animation_data = ColumnDataSource(data=self.line_temp_dict)
        self.graph_under_dict = dict(x=[1, 2, 3, 4], theta=[np.pi, np.pi / 2, np.pi / 3, np.pi / 4],position=[1, 2, 3, 7])
        self.graph_under_cds = ColumnDataSource(data=self.graph_under_dict)
        #end CDS---------------------

        # Set up plot
        self.plot = figure(plot_height=500, plot_width=500, title="Wizualizacja",
                           tools="crosshair,pan,reset,save",
                           x_range=self.x_range, y_range=self.y_range)

        self.ip_base = self.plot.rect('base_x', 'base_y', 'base_h', 'base_w', source=self.ip_animation_data,fill_color='cyan')
        self.ip_line = self.plot.line('line_xs', 'line_ys', source=self.line_animation_data,line_color='black')
        self.ip_ball = self.plot.circle('ball_x', 'ball_y', source=self.ip_animation_data, size='ball_size')

        self.theta_graph = figure(plot_height=250, plot_width=800, title="Theta",
                                  tools="crosshair,pan,reset,save,wheel_zoom")
        self.line_theta = self.theta_graph.line('x', 'theta', source=self.graph_under_cds)

        self.graph_position = figure(plot_height=250, plot_width=800, title="Pozycja",
                                     tools="crosshair,pan,reset,save,wheel_zoom")
        self.line_position = self.graph_position.line('x', 'position', source=self.graph_under_cds)
        # Set up widgets SLIDERS:
        self.pendulum_mass_slider = Slider(title="Mass of the ball", value=0.2, start=0.1, end=2.0, step=0.1)
        self.cart_mass_slider = Slider(title="Mass of the cart", value=0.5, start=0.1, end=2.0, step=0.1)
        self.gravity_slider = Slider(title="Gravity", value=10.0, start=9.8, end=10.0, step=1)
        self.pendulum_length_slider = Slider(title="Length", value=self.default_pendulum_length, start=0.1, end=1.0, step=0.1)
        self.pendulum_angle_slider = Slider(title="Start Angle", value=0.314, start=-np.pi/2, end=np.pi/2, step=np.pi / 36)
        self.start_cart_position_slider = Slider(title="start_cart_position", value=0.0, start=-10.0, end=10.0, step=1)
        self.target_cart_position_slider = Slider(title="target_cart_position", value=0.0, start=-10.0, end=10.0, step=1)

        #layout+callbacks
        curdoc().title = "Inverted pendulum AK TK RO"
        self.inputs = column(self.pendulum_mass_slider, self.cart_mass_slider, self.gravity_slider, self.pendulum_length_slider, self.pendulum_angle_slider, self.start_cart_position_slider, self.target_cart_position_slider)
        curdoc().add_root(column(row(self.inputs, self.plot), self.theta_graph, self.graph_position))
        curdoc().add_periodic_callback(self.draw_next_frame, 100)
        for w in [self.pendulum_mass_slider,self.cart_mass_slider, self.gravity_slider, self.pendulum_length_slider, self.pendulum_angle_slider, self.start_cart_position_slider, self.target_cart_position_slider]:
            w.on_change('value', self.update_parameters)

        self.update_parameters(0,0,0)

    def draw_next_frame(self):
        if(self.frame>=len(self.angle_results)-1):
            return
        theta = self.angle_results[self.frame]
        print("stopnie obecnie: "+ str(theta/np.pi*180))
        current_cart_position=self.position_results[self.frame]*50
        dx = np.sin(theta) * self.pendulum_length*10
        dy = np.cos(theta) * self.pendulum_length*10

        self.ip_temp_dict['ball_x'] = [current_cart_position + dx]
        self.ip_temp_dict['ball_y'] = [dy]
        self.ip_temp_dict['base_x'] = [current_cart_position]
        self.line_temp_dict['line_xs'] = [current_cart_position, current_cart_position + dx, np.nan, self.target_cart_position,
                                          self.target_cart_position]
        self.line_temp_dict['line_ys'] = [0, dy, np.nan, self.y_range[0], self.y_range[1]]

        self.line_animation_data.data = self.line_temp_dict
        self.ip_animation_data.data = self.ip_temp_dict
        self.frame+=1

    def update_parameters(self,attrname, old, new):
        # Get the current slider values
        self.pendulum_length = self.pendulum_length_slider.value
        self.target_cart_position = self.target_cart_position_slider.value

        gravity = self.gravity_slider.value
        theta0 = self.pendulum_angle_slider.value
        pendulum_mass = self.pendulum_mass_slider.value
        cart_mass = self.cart_mass_slider.value
        x0=self.start_cart_position_slider.value
        x=self.target_cart_position
        cart_rub=0.1
        pendulum_inertia=(self.pendulum_length**2) * pendulum_mass
        theta = 0
        #simulator = FullSimulator.FullSimulator(0.5, 0.1, 0.2, 0.6, 0.006, 0, 0.314, 0, 0, 9.81)
        simulator = FullSimulator.FullSimulator(cart_mass, cart_rub, pendulum_mass, self.pendulum_length, pendulum_inertia, x0, theta0, x, theta, gravity)
        print(cart_mass, cart_rub, pendulum_mass, self.pendulum_length, pendulum_inertia, x0, theta0, x, theta, gravity)
        #(0.5, 0.1, 0.2, 0.6, 0.006, 0, 0, 2, 0, 9.81)
        simulator.simulate()
        self.time_results, self.position_results, self.angle_results = simulator.get_result()
        self.ip_temp_dict['ball_size'] = [pendulum_mass * 10]
        self.frame = 0
        #drawing zaleznosci czasowe (graph_under)
        self.graph_under_dict['x']=self.time_results
        self.graph_under_dict['theta'] = self.angle_results
        self.graph_under_dict['position'] = self.position_results
        self.graph_under_cds.data=self.graph_under_dict
        self.draw_next_frame()
        #print(self.ip_temp_dict)

#dodaćc wykresy położenia i kąta w czasie
    def update_plot(self, attrname, old, new):
        pass




#self.ip_temp_dict = dict(base_x=[0], base_y=[0], base_h=[5], base_w=[0.3], ball_x=[0], ball_y=[-5],ball_size=[20])
#self.ip_animation_data = ColumnDataSource(data=self.ip_temp_dict)

#line_temp_dict=dict(line_xs=[0,0], line_ys=[0,-5])
#line_animation_data= ColumnDataSource(data=line_temp_dict)

test=InvertedPendulumVisualization()

# Set up callbacks
# Set up layouts and add to document
#inputs = column(text, masa, gravity, length, angle)
#curdoc().add_root(row(inputs, plot, width=800))


