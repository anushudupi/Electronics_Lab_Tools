/**
ADC Dma capture
 */

#include <stdio.h>
#include "pico/stdlib.h"
#include "pico/multicore.h"
#include "hardware/adc.h"
#include "hardware/dma.h"
#include "hardware/i2c.h"
//#include "hardware/timer.h"
#include "hardware/gpio.h"
#include <math.h>

#define CAPTURE_CHANNEL 0
#define CAPTURE_DEPTH 8000

// MCP4725 I2C address
#define MCP4725_ADDR 0x60

uint8_t capture_buf1[CAPTURE_DEPTH];
uint8_t capture_buf2[CAPTURE_DEPTH];
char f[10] = "\nabcdefg";

void write_dac(int value) {
    uint8_t data[3];
    data[0] = 0x40;                             // command byte
    data[1] = value >> 4;                       // high byte of value
    data[2] = (value & 0xF)<<4;                     // low byte of value
    i2c_write_blocking(i2c_default, MCP4725_ADDR, data, 3, false);
}

void PGA(int val){

        gpio_put(10, (val & 0x01) ? 1 : 0);
        gpio_put(11, (val & 0x02) ? 1 : 0);
        gpio_put(12, (val & 0x04) ? 1 : 0);
        gpio_put(13, (val & 0x08) ? 1 : 0);

}

void core1_entry(){
    
    while (1)
    {   char buffer[256];
        //scanf("%s", buffer);
        //printf(buffer);
        /* code */
    }
    


}


int main() {
    stdio_set_translate_crlf(&stdio_usb, false);
    stdio_init_all();
    multicore_launch_core1(core1_entry);
    gpio_init(23);
    gpio_set_dir(23, GPIO_OUT);
    gpio_put(23, 1);
    gpio_init(10);
    gpio_set_dir(10, GPIO_OUT);
    gpio_init(11);
    gpio_set_dir(11, GPIO_OUT);
    gpio_init(12);
    gpio_set_dir(12, GPIO_OUT);
    gpio_init(13);
    gpio_set_dir(13, GPIO_OUT);

    // Initialize I2C peripheral
    i2c_init(i2c_default, 100000);
    gpio_set_function(PICO_DEFAULT_I2C_SDA_PIN, GPIO_FUNC_I2C);
    gpio_set_function(PICO_DEFAULT_I2C_SCL_PIN, GPIO_FUNC_I2C);
    gpio_pull_up(PICO_DEFAULT_I2C_SDA_PIN);
    gpio_pull_up(PICO_DEFAULT_I2C_SCL_PIN);


    adc_gpio_init(26 + CAPTURE_CHANNEL);

    adc_init();
    adc_select_input(CAPTURE_CHANNEL);
    adc_fifo_setup(
        true,    // Write each completed conversion to the sample FIFO
        true,    // Enable DMA data request (DREQ)
        1,       // DREQ (and IRQ) asserted when at least 1 sample present
        false,   // We won't see the ERR bit because of 8 bit reads; disable.
        true     // Shift each sample to 8 bits when pushing to FIFO
    );

    // Divisor of 0 -> full speed. Free-running capture with the divider is
    // equivalent to pressing the ADC_CS_START_ONCE button once per `div + 1`
    // cycles (div not necessarily an integer). Each conversion takes 96
    // cycles, so in general you want a divider of 0 (hold down the button
    // continuously) or > 95 (take samples less frequently than 96 cycle
    // intervals). This is all timed by the 48 MHz ADC clock.
    adc_set_clkdiv(0);

    sleep_ms(4000);
    printf("started\n");
    sleep_ms(1000);
    uint dma_chan = dma_claim_unused_channel(true);
    dma_channel_config cfg = dma_channel_get_default_config(dma_chan);

    // Reading from constant address, writing to incrementing byte addresses
    channel_config_set_transfer_data_size(&cfg, DMA_SIZE_8);
    channel_config_set_read_increment(&cfg, false);
    channel_config_set_write_increment(&cfg, true);

    // Pace transfers based on availability of ADC samples
    channel_config_set_dreq(&cfg, DREQ_ADC);


    // Start timer
    int O=2047;
    int O1=2047;
    int G=0;
    int G1=0;
    write_dac(O);
    PGA(G);
    uint8_t mx;
    uint8_t mn;
    int a;

    dma_channel_configure(dma_chan, &cfg,
        capture_buf1,    // dst
        &adc_hw->fifo,  // src
        CAPTURE_DEPTH,  // transfer count
        true            // start immediately
    );


    adc_run(true);
    dma_channel_wait_for_finish_blocking(dma_chan);
    G1=G;
    O1=O;
    
  


    while (1){
    mx = capture_buf1[0];
    mn = capture_buf1[0];

   

    for(int i=1; i<CAPTURE_DEPTH; i++)
    {
        if(capture_buf1[i]>mx)
        {
            mx = capture_buf1[i];
        }


        if(capture_buf1[i]<mn)
        {
            mn = capture_buf1[i];
        }
    }
    if(mx>250||mn<5){
        O=2047;
        G=0;
    }
    else if (fabs((mx+mn)/254-1)>0.02)
    {
      if (((mx+mn)>254))
      {
       O=O-((mx+mn)*2-508);
      }
      else
      {
       O=O+(508-(mx+mn)*2);
      }
    }
    else
    {

      
      for(int i=G+1;i<16;i++){
        if(((i+1)*(mx-mn))>245*(G+1))
        {
         a=i-1;
         break;
        }
        else
        {
         a=i; 
        }
        G=a;

      }
    }
    
    
        write_dac(O);
        PGA(G);
        printf(f);
        printf("%d",G1);
        printf(" ");
        printf("%d",O1);
        printf("\n");

        sleep_ms(1);
        dma_channel_configure(dma_chan, &cfg,
        capture_buf2,    // dst
        &adc_hw->fifo,  // src
        CAPTURE_DEPTH,  // transfer count
        true            // start immediately
    );


    fwrite(&capture_buf1[0],CAPTURE_DEPTH, 1, stdout);
    fflush(stdout);
    //printf("x");
    dma_channel_wait_for_finish_blocking(dma_chan);
    G1=G;
    O1=O;
    mx = capture_buf2[0];
    mn = capture_buf2[0];

   

    for(int i=1; i<CAPTURE_DEPTH; i++)
    {
        if(capture_buf2[i]>mx)
        {
            mx = capture_buf2[i];
        }


        if(capture_buf2[i]<mn)
        {
            mn = capture_buf2[i];
        }
    }
    if(mx>250||mn<5){
        O=2047;
        G=0;
    }
    else if (fabs((mx+mn)/254-1)>0.02)
    {
      if ((float)(mx+mn)/2>127)
      {
       O=O-((mx+mn)*2-508);
      }
      else
      {
       O=O+(508-(mx+mn)*2);
      }
    }
    else
    {

      
      for(int i=G+1;i<16;i++){
        if(((i+1)*(mx-mn))>245*(G+1))
        {
         a=i-1;
         break;
        }
        else
        {
         a=i; 
        }
        G=a;

      }
    }
    
    
        write_dac(O);
        PGA(G);
        printf(f);
        printf("%d",G1);
        printf(" ");
        printf("%d",O1);
        printf("\n");

     
     sleep_ms(1);   
        dma_channel_configure(dma_chan, &cfg,
        capture_buf1,    // dst
        &adc_hw->fifo,  // src
        CAPTURE_DEPTH,  // transfer count
        true            // start immediately
    );

    
    
    fwrite(&capture_buf2[0],CAPTURE_DEPTH, 1, stdout);
    fflush(stdout);


    dma_channel_wait_for_finish_blocking(dma_chan);
    G1=G;
    O1=O;
    

    
    }
}
