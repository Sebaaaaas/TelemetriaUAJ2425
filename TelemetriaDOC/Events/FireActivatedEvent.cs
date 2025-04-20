using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class FireActivatedEvent:Event
    {
        public FireActivatedEvent(float timestamp) : base(timestamp)
        {
            name = "FireActivatedEvent";
        }
        public override string serializeToJSON()
        {
            string s = "{";
            s += base.serializeToJSON();
            s += ", ";
            s += "\"FireActivated\" : " + true;
            s += "}";
            return s;
        }
    }
}
