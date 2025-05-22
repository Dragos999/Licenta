import ctypes

ctypes.windll.user32.SetProcessDPIAware(1)

screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

initial_x = screen_width - 70
initial_y = screen_height - 140

xratio = screen_width / 1920
yratio = screen_height / 1080
