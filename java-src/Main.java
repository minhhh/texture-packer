import org.python.core.PyException;
import org.python.util.PythonInterpreter;
import org.python.core.Py;
import org.python.core.PySystemState;
import org.python.core.PyString;

public class Main {
    public static void main(String[] args) throws PyException{
        String[] argv = new String[args.length + 1];
        argv[0] = "";
        System.arraycopy(args, 0, argv, 1, args.length);
        PySystemState.initialize(PySystemState.getBaseProperties(), null, argv);

        PythonInterpreter intrp = new PythonInterpreter(null, new PySystemState());
        PySystemState sys = Py.getSystemState();
        sys.path.append(new PyString("__pyclasspath__/libpython/"));

        intrp.exec("import main");
        intrp.exec("main.main()");
    }
}
