using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace TelemetriaDOC
{
    // Objetivo: Abrir archivo, recoger del serializador el texto a escribir en el documento, escribirlo en el documento y al acabar cerrar archivo

    // en ppo el serializador nos devolvera una linea por cada evento
    class DiskPersistence : Persistence
    {
        private string persistanceFileName;
        private StreamWriter file;
        public DiskPersistence(string persistanceFileName_, Serializer serializer_)
        {
            persistanceFileName = persistanceFileName_ + serializer_.getExtension();
            file = new StreamWriter(persistanceFileName, true);
        }

        ~DiskPersistence()
        {
            file.Close();
        }

        public void close()
        {
            file.Close();
        }

        public void persist()
        {
            file.WriteLine("text");
            file.Flush();
            throw new NotImplementedException();
        }
    }
}
