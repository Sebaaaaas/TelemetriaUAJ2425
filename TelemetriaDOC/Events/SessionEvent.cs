using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class SessionEvent : Event
    {
        public enum EventType { SessionStart, SessionEnd };
        EventType _type;
        public SessionEvent(float timestamp, EventType type) : base(timestamp)
        {
            _type = type;
            name = _type.ToString();
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
