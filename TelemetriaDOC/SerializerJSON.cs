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
        public string Serialize(Event e)
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
            s += e.SerializeToJSON();
            return s;
            
        }
        public string GetExtension()
        {
            return ".json";
        }
        public string SerializerEnding()
        {
            return "\n]\n";
        }
    }
}
