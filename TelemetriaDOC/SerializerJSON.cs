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
            if (firstTime)
            {
                firstTime = false; 
                return "[\n"+ e.serializeToJSON()+",\n";
            }
            else
            {
                return e.serializeToJSON()+",\n";
            }
            
        }
        public string getExtension()
        {
            return ".json";
        }
        public string closeJson()
        {
            return "\n]\n";
        }
    }
}
