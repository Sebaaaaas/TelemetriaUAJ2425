using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace TelemetriaDOC
{
    class ArchivePers:Persistence
    {
        private string _name;
        private StreamWriter file;
        public ArchivePers(string name, Serializer serializer) {
            _name = name+serializer.getExtension();
            file =new StreamWriter(_name,true);
            file.WriteLine("Hello");
            //Quitar mas alante
            close();

        }
        public void close()
        {
            file.Close();
        }
    }
}
