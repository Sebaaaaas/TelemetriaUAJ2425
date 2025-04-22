using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC.Events
{
    public class Puzzle2ResetEvent : Event
    {
        public Puzzle2ResetEvent(float timestamp) : base(timestamp)
        {
            name = "Puzzle2ResetEvent";
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
