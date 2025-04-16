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

        public static bool Init()
        {
            if (instance != null)
                return false;

            instance= new Tracker();

            //Iniciar serializador
            instance.initSerializer(Format.JSON);

            //Iniciar persistencia
            instance.initPersistence(Type.Archive, "prueba");

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
                case Type.Archive:
                    persistence = new ArchivePers(name, serializer);
                    break;
            }
        }

        public static void TrackEvent(Event e) {

            instance.persistence.write(instance.serializer.serialize(e));

        }

        public static void closing()
        {
            instance.CloseArch();
        }
        private void CloseArch()
        {
            persistence.close();
        }

    }
}
