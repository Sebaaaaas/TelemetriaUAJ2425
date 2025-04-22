using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class PlayerAttackEvent : Event
    {
        public PlayerAttackEvent(float timestamp) : base(timestamp)
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
