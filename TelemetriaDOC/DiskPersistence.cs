using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace TelemetriaDOC
{
    class DiskPersistence : Persistence
    {
        private string persistanceFileName;
        private StreamWriter file;
        public DiskPersistence(string persistanceFileName_, Serializer serializer_)
        {
            persistanceFileName = persistanceFileName_ + serializer_.getExtension();
            file = new StreamWriter(persistanceFileName, false);
        }

        public override void write(string s)
        {
            file.WriteLine(s);
        }

        public override void close()
        {
            file.Close();
        }
    }
}
