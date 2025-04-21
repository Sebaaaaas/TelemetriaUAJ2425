using System;
using System.Collections.Generic;
using System.Text;
using System.Xml.Linq;

namespace TelemetriaDOC.Events
{
    public class Puzzle2SuccessEvent:Event
    {
        public Puzzle2SuccessEvent(float timestamp) : base(timestamp)
        {
            name = "Puzzle2SuccessEvent";
        }

        public override string serializeToJSON()
        {
            string s = "{";
            s += base.serializeToJSON();
            s += "}";
            return s;
        }
    }
}
