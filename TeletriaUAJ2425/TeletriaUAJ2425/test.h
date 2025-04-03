#pragma once

#define DLLExport __declspec (dllexport)

// o podemos intentar exportar clases o exportar una funcion trackEvent y exportar tambien
// Tener un script genérico con funciones genéricas exportadas que dentro de ellas utilicen las clases nuestras de c++

extern "C"
{
	DLLExport int hi();

}

