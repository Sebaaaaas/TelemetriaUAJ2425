﻿using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public class SessionEvent : Event
    {
        public enum EventType { SessionStart, SessionEnd };
        EventType _type;
        public SessionEvent(EventType type)
        {
            _type = type;
            name = _type.ToString();
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
