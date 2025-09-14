import astro_constants
import astro_functions
import subprocess

# Initialise display
inky_display, base_img, display_height, display_width, draw = astro_functions.init_display()

#image
image = astro_functions.load_svg_icon(astro_functions.config['about']['image'], size=astro_constants.icon_size_xl)
base_img.paste(image, ((display_width // 2) - (astro_constants.icon_size_xl[0] // 2), (display_height // 2) - (astro_constants.icon_size_xl[0] // 2) + 50))

#message
align_center = display_width // 2
astro_banner = "This is AstroInky!"
banner_center = align_center - (draw.textlength(astro_banner, font=astro_constants.font_large) / 2)
message_top = astro_functions.config['about']['top_msg']
top_center = align_center - (draw.textlength(message_top, font=astro_constants.font_large) / 2)
message_mid = astro_functions.config['about']['mid_msg']
mid_center = align_center - (draw.textlength(message_mid, font=astro_constants.font) / 2)
message_footer = astro_functions.config['about']['low_msg']
footer_center = align_center - (draw.textlength(message_footer, font=astro_constants.font) / 2)

draw.text((banner_center, 120), astro_banner, astro_constants.BLACK, font=astro_constants.font_large)
draw.text((top_center, 300), message_top, astro_constants.BLACK, font=astro_constants.font_large)
draw.text((mid_center, 600), message_mid, astro_constants.RED, font=astro_constants.font)
draw.text((footer_center, 600 + (astro_constants.font_height * 2)), message_footer, astro_constants.GREEN, font=astro_constants.font)

# Status Text
yes_words = ('y', 'Y','yes','Yes','YES',1,'true','True',True)
if astro_functions.config['about']['show_wifi'] in yes_words:
  cmd = "iwgetid -r"
  message_ssid = "SSID: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
  ssid_center = (align_center // 2) - (draw.textlength(message_ssid.rstrip(), font=astro_constants.font_small) //2)
  draw.text((ssid_center, 600+  (astro_constants.font_height * 5)), message_ssid, astro_constants.BLUE, font=astro_constants.font_small)

if astro_functions.config['about']['show_ip'] in yes_words:
  cmd = "hostname -I | cut -d' ' -f1"
  message_ip = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
  ip_center = (align_center + (align_center // 2)) - (draw.textlength(message_ip.rstrip(), font=astro_constants.font_small) //2)
  draw.text((ip_center, 600+  (astro_constants.font_height * 5)), message_ip, astro_constants.BLUE, font=astro_constants.font_small)

if astro_functions.config['global']['use_battery'] in yes_words:
  import ina219
  # Create an INA219 instance.
  ups_hat = ina219.ina219(addr=0x43)
  bus_voltage = ups_hat.getBusVoltage_V()             # voltage on V- (load side)
  current = ups_hat.getCurrent_mA()                   # current in mA
  power = ups_hat.getPower_W()                        # power in W
  p = (bus_voltage - 3)/1.2*100
  if(p > 100):p = 100
  if(p < 0):p = 0
  message_batp = "Battery: " + str(round(p)) + "%"
  batp_center = align_center - (draw.textlength(message_batp, font=astro_constants.font_small) / 2)
  draw.text((batp_center, 600+  (astro_constants.font_height * 6)), message_batp, astro_constants.BLUE, font=astro_constants.font_small)

#FINAL DISPLAY
astro_functions.astro_display(base_img, inky_display)
