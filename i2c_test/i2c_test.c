#include "stdio.h"
#include "pico/stdlib.h"
#include "hardware/i2c.h"

// MCP4725 I2C address
#define MCP4725_ADDR 0x60

// Function to write a value to the MCP4725 DAC
void write_dac(uint16_t value) {
    uint8_t data[3];
    data[0] = 0x40;                             // command byte
    data[1] = value >> 4;                       // high byte of value
    data[2] = (value & 0xF)<<4;                     // low byte of value
    i2c_write_blocking(i2c_default, MCP4725_ADDR, data, 3, false);
}

int main() {
    stdio_init_all();
    sleep_ms(1000);
    printf("helloworld");

    // Initialize I2C peripheral
    i2c_init(i2c_default, 100000);
    gpio_set_function(PICO_DEFAULT_I2C_SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(PICO_DEFAULT_I2C_SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(PICO_DEFAULT_I2C_SDA_PIN);
    gpio_pull_up(PICO_DEFAULT_I2C_SCL_PIN);
 printf("\n1");
    // Set the output voltage to 1V
    uint16_t output_value = 4095;
    write_dac(output_value);
printf("\n2");
    

    while (true) {
        // Do something interesting here...
    }

    return 0;
}
