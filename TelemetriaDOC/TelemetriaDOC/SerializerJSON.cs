using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class SerializerJSON : Serializer
    {
        public string serialize()
        {
            return "Hello JSON";
        }
        public string getExtension()
        {
            return ".json";
        }
    }
}
