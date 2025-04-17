using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class FireActivatedEvent:Event
    {
        public FireActivatedEvent(float timestamp) : base(timestamp)
        {
           
        }
        public override string getName() { return "FireActivated"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"FireActivated\" : " + true;
            s += "\n  }";
            return s;
        }
    }
}
