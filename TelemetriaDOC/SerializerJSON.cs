using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class SerializerJSON : Serializer
    {
        bool firstTime = true;
        public string serialize(Event e)
        {
            string s="";
            if(firstTime)
            {
                 s += "{\n";
            }
            s+= e.serializeToJSON();
            return s;
        }
        public string getExtension()
        {
            return ".json";
        }
        public string closeJson()
        {
            return "\n}\n";
        }
    }
}
