using System;
using System.Collections.Generic;
using System.Text;

namespace TelemetriaDOC
{
    public enum Type {Disk}
    interface Persistence
    {
        void persist();
    }
}
