using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class SessionEvent : Event
    {
        public enum EventType { SessionStart, SessionEnd };
        EventType _type;
        public SessionEvent(Guid id_session, int timestamp, EventType type) : base(id_session, timestamp)
        {
            _type = type;
        }

        public override string getName() { return "SessionEvent"; }
        public override string serializeToJSON()
        {
            string s = "  {\n";
            s += base.serializeToJSON();
            s += ",\n";
            s += "    \"Type\" : " + _type.ToString();
            s += "\n  }\n";
            return s;
        }
    }
}
