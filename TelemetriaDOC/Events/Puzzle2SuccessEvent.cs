using System;
using System.Collections.Generic;
using System.Text;
using System.Xml.Linq;

namespace TelemetriaDOC.Events
{
    public class Puzzle2SuccessEvent:Event
    {
        public Puzzle2SuccessEvent()
        {
            name = "Puzzle2SuccessEvent";
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
