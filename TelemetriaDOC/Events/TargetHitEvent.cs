using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class TargetHitEvent:Event
    {
        private string hitterTag;
        public TargetHitEvent(float timestamp, string _hitterTag) : base(timestamp)
        {
            hitterTag = _hitterTag;
            name = "TargetHitEvent";
        }
        public override string serializeToJSON()
        {
            string s = "{";
            s += base.serializeToJSON();
            s += ", ";
            s += "\"Hitter\" : \"" + hitterTag+ "\"";
            s += "}";
            return s;
        }
    }
}
