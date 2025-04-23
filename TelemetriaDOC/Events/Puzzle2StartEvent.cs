using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class Puzzle2StartEvent : Event
    {
        public Puzzle2StartEvent()
        {
            name = "Puzzle2StartEvent";
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
