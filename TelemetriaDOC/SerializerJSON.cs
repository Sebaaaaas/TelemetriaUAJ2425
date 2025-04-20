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
            //if (firstTime)
            //{
            //    firstTime = false; 
            //    return "[\n"+ e.serializeToJSON()+",\n";
            //}
            //else
            //{
            //    return e.serializeToJSON()+",\n";
            //}
            
        }
        public string getExtension()
        {
            return ".json";
        }
        public string close()
        {
            return "\n]\n";
        }
    }
}
