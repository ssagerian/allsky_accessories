#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "dew_heater_control.h"

int main(void)
{
   char * dew_heater_var = "DEW_HEATER_CONTROL_ENV_VAR"; 
   char env_var[20];
   char local_var[20];
   memset(local_var, 0,20);
   char * p_get_env = NULL;
   p_get_env = getenv(dew_heater_var); 
   if (NULL == p_get_env)
   {
      printf("my env is not set %s\n", dew_heater_var);
      exit(1);
   }
   else
   {
      printf("my env is set to %s \n", p_get_env);
      strcpy(local_var, p_get_env);
   }
   while (1)
   {
      
      p_get_env = getenv(dew_heater_var); 
      if (0 != strcmp(p_get_env, local_var)) 
      {
         printf("my env is set to %s \n", p_get_env);
         memset(local_var, 0,20);
         strcpy(local_var, p_get_env);
      }
      else
      {
         printf(".\n");
      }
   }
   return 0; 
}
      
