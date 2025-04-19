using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class PlayerAttackEvent : Event
    {
        public PlayerAttackEvent(float timestamp) : base(timestamp)
        {

        }
        public override string getName() { return "PlayerAtack"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"PlayerAtack\" : " + true;
            s += "\n  }";
            return s;
        }
    }
}
