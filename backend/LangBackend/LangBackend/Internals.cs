namespace LangBackend;

public partial class Interpreter
{
    private class ClassDefinition
    {
        public string Name { get; }
        public Dictionary<string, string> Fields { get; }
        public Dictionary<string, FunctionDefinition> Methods { get; }

        public ClassDefinition(string name)
        {
            this.Name = name;
            this.Fields = new Dictionary<string, string>();
            this.Methods = new Dictionary<string, FunctionDefinition>();
        }
    }
    
    private class FunctionDefinition
    {
        public int ParamsCount { get; set; }
        public List<string> Params { get; set; }
        public List<Token> Body { get; set; }

        public FunctionDefinition(int paramsCount, List<string> parameters, List<Token> body)
        {
            this.ParamsCount = paramsCount;
            this.Params = parameters;
            this.Body = body;
        }
    }
    
    private class Reference
    {
        public Reference()
        {
            
        }
    }
    
}