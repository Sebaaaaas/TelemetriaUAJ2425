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
            

        }
        public override void write(string s)
        {
            file.WriteLine(s);
            close();
        }
        public void close()
        {
            file.Close();
        }
    }
}
