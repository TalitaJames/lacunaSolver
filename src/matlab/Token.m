classdef Token

    properties
        x {mustBeNumeric}
        y {mustBeNumeric}
        token
    end

   enumeration
      LightBlue ("#4DBEEE"), DarkBlue, Yellow, Red, Pink, Purple, Brown
   end
   methods
       function obj = Token(x,y,token)
            obj.x = x;
            obj.y = y;
            obj.token = token;
       end
       function colorString = toColour(tokenEnum)
           switch tokenEnum
               case Token.LightBlue
                   colorString = "#4DBEEE";

               case Token.DarkBlue
                   colorString = "#0072BD";

               case Token.Yellow
                   colorString = "#EDB120";
               
               case Token.Red
                   colorString = "#A2142F";

               case Token.Pink
                   colorString = "#ff33ff";
               
               case Token.Purple
                   colorString = "#7E2F8E";
               
               case Token.Brown
                   colorString = "#77AC30";
           end
       end
   end
end
