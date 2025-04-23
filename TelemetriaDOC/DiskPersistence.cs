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
        public DiskPersistence()
        {
            
        }

        public bool Init(string persistanceFileName_, Serializer serializer_)
        {
            try
            {
                persistanceFileName = persistanceFileName_ + serializer_.GetExtension();
                file = new StreamWriter(persistanceFileName, false);
            }
            catch (Exception e)
            {
                return false;
            }

            return true;
        }

        public override void Write(string s)
        {
            file.Write(s);
        }

        public override void Close()
        {
            file.Close();
        }
    }
}
