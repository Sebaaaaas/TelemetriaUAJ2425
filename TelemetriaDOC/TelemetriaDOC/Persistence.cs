using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public enum Type {Disk}
    public abstract class Persistence
    {
        void persist() { }

        public virtual void write(string s) { }

        public virtual void close() { }
    }
}
