using System;
using System.Collections.Generic;

namespace TelemetriaDOC
{
    public class Tracker
    {
        private static Tracker instance = null;
        private Serializer serializer;
        private Persistence persistence;
        
        private Tracker()
        {
        }

        public static Tracker Instance()
        {
            return instance;
        }

        // Format hace referencia a .json, .yaml...
        // PersistenceType hace referencia a si vamos a persistir los datos en disco
        public static bool Init(Format format_, Type persistenceType_)
        {
            if (instance != null)
                return false;

            instance = new Tracker();

            //Iniciar serializador
            instance.initSerializer(format_);

            //Iniciar persistencia
            instance.initPersistence(persistenceType_, "prueba");

            return true;
        }

        public void initSerializer(Format format)
        {
            switch(format)
            {
                case Format.JSON:
                    serializer = new SerializerJSON();
                    break;
            }
        }

        public void initPersistence(Type typeSave,string name) {
            switch (typeSave)
            {
                case Type.Disk:
                    persistence = new DiskPersistence(name, serializer);
                    break;
            }
        }

        public void TrackEvent(Event e) { persistence.persist(); }
    }
}
