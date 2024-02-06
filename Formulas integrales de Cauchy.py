from sympy import I, sympify, fraction, factor, divisors, poly, symbols, roots, factor_list, pi
import os
import sys
import numpy as np

def clear_screen():
   if os.name == 'posix':  # Linux
      os.system('clear')
   elif os.name == 'nt':  # Windows
      os.system('cls')
   else:
      print("No se puede borrar la pantalla en este sistema operativo.")


def es_formato_cociente(expresion):
   try:
      # Intenta crear una expresión simbólica con la entrada
      expr = sympify(expresion)
      numerador, denominador = fraction(expr)

      # Verifica si tanto el numerador como el denominador son polinomios
      numerador_poly = poly(numerador)
      denominador_poly = poly(denominador)

      # ######### debugeo mio para ver si se guardaban bien las expresiones del num y denum
      # print(numerador_poly)
      # print(denominador_poly)

      if numerador_poly is not None and denominador_poly is not None:
         return True
      else:
         return False
   except Exception as e:
      print(f"Error: {e}")
      return False
   

# Crea una lista de los factores de una expresion
def array_factors(expresion):
   # Definir símbolos
   z = symbols('z')
   
   # Obtener las raíces
   raices = roots(expresion, z)
   # Obtener la lista de las raíces (claves del diccionario)
   lista_values = list(raices.values())
   # print(raices)
   # print(lista_values) #apariciones de la raiz, lo uso para exponentes en el array que retorna
   
   # Construir los factores manualmente por los exponentes de los factores
   factores_parcial = [z - raiz for raiz in raices]
   factores = [(elem)**potencia for elem, potencia in zip(factores_parcial, lista_values)]

   return factores


def max_exponent(expresion):
   z = symbols('z')
   raices = roots(expresion, z)
   lista_values = list(raices.values())

   maximo_exponente = max(lista_values)
   return maximo_exponente


def factor_in(denom_factors, raices, r, zo):
   result_factors = []
   for factor, raiz in zip(denom_factors, raices):
      if abs(raiz - zo) <= r: # verificamos que los puntos raices esten dentro de C
         result_factors.append(factor)
   return result_factors

def point_eval(denom_factors, raices, r, zo):
   point_evaluate = []
   for factor, raiz in zip(denom_factors, raices):
      if abs(raiz - zo) <= r: # verificamos que los puntos raices esten dentro de C
         point_evaluate.append(raiz)
   return point_evaluate

def new_function(numerador_original, denominador_original, factores_huecos):
   if len(factores_huecos) == 1:
      new_denom = factor(denominador_original)/factor(factores_huecos[0])
      if new_denom is not None:
         new_functi = numerador_original/factor(new_denom)
         return new_functi
      else:
         print("Error al factorizar el nuevo denominador.")
   else:
      print("Valio chetos, hay más de un hueco, usar el teorema")
      return



def cauchy(funshion, point_eval, n):
   z = symbols('z')
   if n == 0:
      result = funshion.subs(z, point_eval)
   else:
      derivada_n = funshion.diff(z, n)
      result = derivada_n.subs(z, point_eval)
   return 2 * pi * I * result

if __name__ == "__main__":
   z = symbols('z')
   entrada_integral = input("Ingrese la expresión de la integral en forma de cociente: ")

   # Verifica si la entrada está en el formato correcto
   if es_formato_cociente(entrada_integral):
      numerador, denominador = fraction(sympify(entrada_integral))
   
      print("La expresión es un cociente. Puedes continuar con el programa.")

      print("\nInserte el centro z0 del circulo de convergencia. |z-z0| = R")
      print("Nota: utiliza el caracter I (i mayuscula) para denotar la unidad imaginaria.\n")
      centro_circulo = sympify(input("Inserte el centro z0 del círculo de convergencia: "))
      radio_circulo = float(input("Inserte el radio de convergencia R: "))

      denom_factors = array_factors(str(denominador))
      raices = roots(str(denominador), z)
      ind_points = list(raices.keys())
      print(denom_factors)
      print(ind_points)

      raices_dentro_de_c = factor_in(denom_factors, raices, radio_circulo, centro_circulo)
      punto_a_evaluar = point_eval(denom_factors, raices, radio_circulo, centro_circulo)
      print(raices_dentro_de_c)
      print(punto_a_evaluar)
      num_huecos = len(raices_dentro_de_c)
      print(num_huecos)

      #clear_screen()
      print(f"F(z) = {entrada_integral}")
      print(f"C: |z - ({centro_circulo})| = {radio_circulo}")

      if num_huecos == 0:
         print("VALOR DE LA INTEGRAL DE CAUCHY: 0")
         print("NO HAY HUECOS EN LA REGION ANALITICA")
         sys.exit()


      new_f = new_function(numerador, denominador, raices_dentro_de_c)

      if new_f is not None:
         new_fz = sympify(new_f)

         print("MAX XPT IN DENOMINADOR")
         max_exp = max_exponent(str(denominador))
         print(max_exp)
         n_for_deriv = max_exp-1

         print("NUEVA FUN")
         print(new_fz)

         # Convertir los elementos de punto_a_evaluar a números complejos
         punto_a_evaluar = [complex(elem.evalf()) for elem in punto_a_evaluar]

         # akiiiiiiiiiiiiiiii kalcular el valor
         integral_value = cauchy(new_fz, punto_a_evaluar[0], n_for_deriv)

         print(integral_value)

   else:
      print("La expresión no está en formato de cociente. Por favor, ingresa una expresión válida.")