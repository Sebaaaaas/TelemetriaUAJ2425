using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class FireActivatedEvent:Event
    {
        public FireActivatedEvent()
        {
            name = "FireActivatedEvent";
        }
        public override string SerializeToJSON()
        {
            string s = "{";
            s += base.SerializeToJSON();
            s += "}";
            return s;
        }
    }
}
