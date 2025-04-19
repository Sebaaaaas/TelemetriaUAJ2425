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
        }
        public override string getName() { return "HitterTag"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"Hitter\" : " + hitterTag;
            s += "\n  }";
            return s;
        }
    }
}
