using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public enum Type {Archive}
    abstract class Persistence
    {
        public virtual void write(string s) { }

        public virtual void close() { }
    }
}
