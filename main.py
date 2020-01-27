import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, Button
from bokeh.plotting import figure
# data from simulation
from Simulation import FullSimulator, RealTimeSimulator


class InvertedPendulumVisualization:
    def __init__(self):
        # Set up data - defaults
        # mind that only some of those are NOT updated after launch ever again
        self.pendulum_angle = 0.314
        self.pendulum_mass = 0.2
        self.cart_mass = 0.5
        self.pendulum_length = 0.6
        self.gravity = 10
        self.start_cart_position = 0
        self.target_cart_position = 1

        # other
        self.frame_time = 20
        self.debug = True
        self.frame = 0
        self.y_range = [-15, 15]  # temp for target line
        self.time_results, self.position_results, self.angle_results = ([], [], [])

        # CDS-przechowuja zmieniajace sie dane i automatycznie akutualizuja wykres-------------------------------------
        self.ip_temp_dict = dict(base_x=[0], base_y=[0], base_h=[5], base_w=[0.3], ball_x=[0], ball_y=[-5],
                                 ball_size=[10])
        self.ip_animation_data = ColumnDataSource(data=self.ip_temp_dict)
        self.line_temp_dict = dict(line_xs=[0, 0], line_ys=[0, -5])
        self.line_animation_data = ColumnDataSource(data=self.line_temp_dict)
        self.graph_under_dict = dict(x=[1, 2, 3, 4], theta=[np.pi, np.pi / 2, np.pi / 3, np.pi / 4],
                                     position=[1, 2, 3, 7])
        self.graph_under_cds = ColumnDataSource(data=self.graph_under_dict)

        # Set up animation drawing
        self.animation = figure(plot_height=500, plot_width=1000, title="Wizualizacja",
                                tools="crosshair,pan,reset,save",
                                x_range=[-30, 30], y_range=[-15, 15])
        self.animation_base = self.animation.rect(
            'base_x', 'base_y', 'base_h', 'base_w', source=self.ip_animation_data, fill_color='cyan')
        self.animation_line = self.animation.line(
            'line_xs', 'line_ys', source=self.line_animation_data, line_color='black')
        self.animation_ball = self.animation.circle(
            'ball_x', 'ball_y', source=self.ip_animation_data, size='ball_size')

        # setup graphs under animation
        self.plot_theta = figure(
            plot_height=250, plot_width=800, title="Theta",
            tools="crosshair,pan,reset,save,wheel_zoom")  # y_range=[-np.pi*1.1, np.pi*1.1]
        self.plot_line_theta = self.plot_theta.line(
            'x', 'theta', source=self.graph_under_cds)
        self.plot_position = figure(
            plot_height=250, plot_width=800, title="Pozycja", tools="crosshair,pan,reset,save,wheel_zoom")
        self.plot_line_position = self.plot_position.line(
            'x', 'position', source=self.graph_under_cds)
        plots_list = [self.plot_theta, self.plot_position]

        # Set up widgets-> SLIDERS:
        self.pendulum_mass_slider = Slider(
            title="Mass of the ball", value=self.pendulum_mass, start=0.1, end=2.0, step=0.1)
        self.cart_mass_slider = Slider(
            title="Mass of the cart", value=self.cart_mass, start=0.1, end=2.0, step=0.1)
        self.gravity_slider = Slider(
            title="Gravity", value=self.gravity, start=8, end=12.0, step=0.1)
        self.pendulum_length_slider = Slider(
            title="Length", value=self.pendulum_length, start=0.5, end=1.0, step=0.1)
        self.pendulum_angle_slider = Slider(
            title="Start Angle", value=self.pendulum_angle, start=-np.pi / 2, end=np.pi / 2, step=np.pi / 36)
        self.start_cart_position_slider = Slider(
            title="start_cart_position", value=self.start_cart_position, start=-10.0, end=10.0, step=1)
        self.target_cart_position_slider = Slider(
            title="target_cart_position", value=0.0, start=-10.0, end=10.0, step=1)
        slider_list = [self.pendulum_mass_slider, self.cart_mass_slider, self.gravity_slider,
                       self.pendulum_length_slider, self.pendulum_angle_slider, self.start_cart_position_slider,
                       self.target_cart_position_slider]
        self.przycisk = Button(label="Simulate")
        self.przycisk.on_click(self.przycisk_handler)
        # layout
        curdoc().title = "Inverted pendulum AK TK RO"
        self.inputs = column(children=slider_list + [self.przycisk])
        curdoc().add_root(column(children=[row(self.inputs, self.animation)] + plots_list))

        self.update_parameters(0, 0, 0)
        # callbacks

        curdoc().add_periodic_callback(self.draw_next_frame, self.frame_time)
        # for w in [self.pendulum_mass_slider, self.cart_mass_slider, self.gravity_slider, self.pendulum_length_slider,
        #          self.pendulum_angle_slider, self.start_cart_position_slider, self.target_cart_position_slider]:
        #    w.on_change('value', self.update_parameters)

    def przycisk_handler(self, test):
        self.update_parameters(0, 0, 0)

    def draw_next_frame(self):
        # if self.frame >= len(self.angle_results) - 1:
        #    return
        # theta = self.angle_results[self.frame]
        # current_cart_position = self.position_results[self.frame]
        self.simulator.set_target_position(self.target_cart_position_slider.value)
        self.simulator.simulate()
        a, b, c = self.simulator.get_result()
        print(a, b, c)
        self.time_results.append(a)
        self.position_results.append(b)
        self.angle_results.append(c)
        theta = c
        current_cart_position = b

        if self.debug:
            print("stopnie obecnie: " + str(theta / np.pi * 180))

        dx = np.sin(theta) * self.pendulum_length * 10
        dy = np.cos(theta) * self.pendulum_length * 10

        self.ip_temp_dict['ball_x'] = [current_cart_position + dx]
        self.ip_temp_dict['ball_y'] = [dy]
        self.ip_temp_dict['base_x'] = [current_cart_position]
        self.line_temp_dict['line_xs'] = [current_cart_position, current_cart_position + dx, np.nan,
                                          self.target_cart_position, self.target_cart_position]
        self.line_temp_dict['line_ys'] = [0, dy, np.nan, self.y_range[0], self.y_range[1]]

        self.line_animation_data.data = self.line_temp_dict
        self.ip_animation_data.data = self.ip_temp_dict
        self.graph_under_dict['x'] = self.time_results
        self.graph_under_dict['theta'] = self.angle_results
        self.graph_under_dict['position'] = self.position_results
        self.graph_under_cds.data = self.graph_under_dict

    def update_parameters(self, attrname, old, new):
        # Get the current slider values
        self.pendulum_length = self.pendulum_length_slider.value
        self.target_cart_position = self.target_cart_position_slider.value
        self.gravity = self.gravity_slider.value

        theta0 = self.pendulum_angle_slider.value
        pendulum_mass = self.pendulum_mass_slider.value
        cart_mass = self.cart_mass_slider.value
        x0 = self.start_cart_position_slider.value
        x = self.target_cart_position
        cart_rub = 0.1
        pendulum_inertia = (self.pendulum_length ** 2) * pendulum_mass
        theta = 0
        # simulator = FullSimulator.FullSimulator(0.5, 0.1, 0.2, 0.6, 0.006, 0, 0.314, 0, 0, 9.81, tk=50, tp=0.01)
        self.simulator = RealTimeSimulator.RealTimeSimulator(cart_mass, cart_rub, pendulum_mass, self.pendulum_length,
                                                             pendulum_inertia, x0, theta0, x, theta, self.gravity)
        print(cart_mass, cart_rub, pendulum_mass, self.pendulum_length, pendulum_inertia, x0, theta0, x, theta,
              self.gravity)
        # (0.5, 0.1, 0.2, 0.6, 0.006, 0, 0, 2, 0, 9.81)
        self.simulator.start()
        self.time_results, self.position_results, self.angle_results = self.simulator.get_result()
        self.time_results = [self.time_results]
        self.position_results = [self.position_results]
        self.angle_results = [self.angle_results]
        self.ip_temp_dict['ball_size'] = [pendulum_mass * 10]
        self.frame = 0

        # drawing zaleznosci czasowe (graph_under) ->
        # update xyranges
        # time_min = min(self.time_results)
        # time_max = max(self.time_results)
        # pos_min = min(self.position_results)
        # pos_max = max(self.position_results)

        # self.plot_position.y_range = Range1d(pos_min, pos_max)
        # self.plot_position.y_range = Range1d(pos_min, pos_max)
        # self.animation.x_range = Range1d(pos_min-10, pos_max+10) # fix it maybe
        # update CDS

        self.draw_next_frame()
        # print(self.ip_temp_dict)


test = InvertedPendulumVisualization()
