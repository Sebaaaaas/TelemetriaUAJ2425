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
        public override string SerializeToJSON()
        {
            string s = "{";
            s += base.SerializeToJSON();
            s += ", ";
            s += "\"Hitter\" : \"" + hitterTag+ "\"";
            s += "}";
            return s;
        }
    }
}
