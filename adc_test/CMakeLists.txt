add_executable(adc_dma_capture
        dma_capture.c
        )

target_link_libraries(adc_dma_capture
		pico_stdlib
		hardware_adc
		hardware_dma
		hardware_i2c
		hardware_gpio
		pico_multicore
		# For the dummy output:
		)
pico_enable_stdio_usb(adc_dma_capture 1)
pico_enable_stdio_uart(adc_dma_capture 0)		




# create map/bin/hex file etc.
pico_add_extra_outputs(adc_dma_capture)

