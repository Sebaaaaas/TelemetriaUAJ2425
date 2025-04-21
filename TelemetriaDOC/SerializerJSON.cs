using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class SerializerJSON : Serializer
    {
        bool firstTime = true;
        public SerializerJSON()
        {
            
        }
        public string serialize(Event e)
        {
            string s = "";
            if (!firstTime)
            {
                s += ",\n";
            }
            else
            {
                s += "[\n";
                firstTime = false;
            }
            s += e.serializeToJSON();
            return s;
            
        }
        public string getExtension()
        {
            return ".json";
        }
        public string serializerEnding()
        {
            return "\n]\n";
        }
    }
}
