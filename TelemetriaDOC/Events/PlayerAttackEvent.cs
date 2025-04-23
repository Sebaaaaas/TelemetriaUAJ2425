using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class PlayerAttackEvent : Event
    {
        public PlayerAttackEvent()
        {
            name = "PlayerAttackEvent";
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
