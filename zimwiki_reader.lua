-- For better performance we put these functions in local variables:
local P, S, R, Cf, Cc, Ct, V, Cs, Cg, Cb, B, C, Cmt =
  lpeg.P, lpeg.S, lpeg.R, lpeg.Cf, lpeg.Cc, lpeg.Ct, lpeg.V,
  lpeg.Cs, lpeg.Cg, lpeg.Cb, lpeg.B, lpeg.C, lpeg.Cmt

local utils = require 'pandoc.utils'

local whitespacechar = S(" \t\r\n")
local specialchar = S("/*~[]\\{}|'_^")
local wordchar = (1 - (whitespacechar + specialchar))
local spacechar = S(" \t")
local tabchar = P"\t" + P"    "
local newline = P"\r"^-1 * P"\n"
local blankline = spacechar^0 * newline
local blanklines = newline * (spacechar^0 * newline)^1
local endline = newline - blanklines
local endequals = spacechar^0 * P"="^0 * spacechar^0 * newline
local cellsep = spacechar^0 * P"|"

local function trim(s)
   return (s:gsub("^%s*(.-)%s*$", "%1"))
end

local function MakeOrderedList(lev, count_type)
  local start
  local subtype
  if count_type == 'A' then
	subtype = 'N'
    start = R('az', 'AZ') * P('.')
  elseif count_type == 'N' then
	subtype = 'A'
    start = R("09")^1 * P('.')
  else
    assert(false)
  end
  local subitem = function(c)
    if lev < 6 then
      return MakeOrderedList(lev + 1, c)
    else
      return (1 - 1) -- fails
    end
  end
  local parser = tabchar^lev
               * #(- tabchar)
			   * start
               * spacechar^1
               * Ct((V"Inline" - (newline * tabchar^0 * (R("09")^1 + R('az', 'AZ')) * P(".")))^0)
               * newline
               * (Ct(subitem(subtype)^1) / pandoc.OrderedList + Cc(nil))
               / function (ils, sublist)
                   return { pandoc.Plain(ils), sublist }
                 end
  return parser
end

local function MakeBulletList(lev)
  local start = P"*"
  local subitem = function()
    if lev < 6 then
      return MakeBulletList(lev + 1)
    else
      return (1 - 1) -- fails
    end
  end
  local parser = tabchar^lev
               * #(- tabchar)
			   * start
               * spacechar^1
               * Ct((V"Inline" - (newline * tabchar^0 * start))^0)
               * newline
               * (Ct(subitem()^1) / pandoc.BulletList + Cc(nil))
               / function (ils, sublist)
                   return { pandoc.Plain(ils), sublist }
                 end
  return parser
end


-- Grammar
G = P{ "Doc",
  Doc = Ct(V"Meta")
      * Ct(V"Block"^0)
      / function(metadata, blocks)
	      return pandoc.Pandoc(blocks, metadata[1])
      end ;
  Block = blankline^0
        * ( V"Header"
          + V"HorizontalRule"
	  + V"IncludeCode"
          + V"CodeBlock"
          + V"CodeBlockPlugin"
          + V"List"
          + V"Table"
	  + V"RawBlock"
          + V"Para");
  Para = Ct((V"Inline")^1)
       * newline
       / pandoc.Para ;
  HorizontalRule = P"--------------------"
                 * newline
                 / pandoc.HorizontalRule;
  Header = (P("=")^1 / string.len)
         * spacechar^1
         * Ct((V"Inline" - endequals)^1)
         * endequals
		 / function(level, content)
			 local result = pandoc.Header(7-level, content)
			 local ident_content = string.lower(pandoc.utils.stringify(content))
			 ident_content = ident_content:gsub(" ", "-")
			 result.attr.identifier = ident_content
			 return result
		   end ;
  CodeBlock = P"'''"
            * newline
            * C((1 - (newline * P"'''"))^0)
            * newline
            * P"'''"
            / pandoc.CodeBlock;
  CodeBlockPlugin = P"{{{code:"
  			* (P' lang="' * C((wordchar - P'"')^1) * P'"')^-1
			* (P' linenumbers="' * C(P'True' + P'False') * P'"')^-1
            * newline
            * C((1 - (newline * P"}}}"))^0)
            * newline
            * P"}}}"
            / function(lang, linenumbers, content)
				local numberLines
				if linenumbers == "True" then
					numberLines = "numberLines"
				else
					numberLines = ""
				end
				return pandoc.CodeBlock(content, {class= lang .. " " .. numberLines})
			  end;
  List = V"BulletList"
       + V"OrderedList" ;
  BulletList = Ct(MakeBulletList(0)^1)
             / pandoc.BulletList ;
  OrderedList = Ct(MakeOrderedList(0,'N')^1)
              / pandoc.OrderedList ;
  IncludeCode = P"[["
       * C((1 - (P"]]" + P"|"))^0)
       * (P"|CODE: " * Ct((V"Inline" - P"]]")^1))^1
	   * P"]]"
       / function(url, desc)
           return pandoc.RawBlock(utils.stringify(desc), url)
         end ;
  Table = V"TableHeader"
        * V"SeparatorRow"
        * Ct(V"TableRow"^1)
        / function(headrow, seprow, bodyrows)
            local numcolumns = #(bodyrows[1])
            local aligns = {}
            local widths = {}
            for i = 1,numcolumns do
			  local a_string = seprow[i][1].content[1].text
			  local a_left  = string.sub(a_string, 1, 1)
			  local a_right = string.sub(a_string, #a_string, #a_string)
			  if a_left == ':' and a_right == '-' then
              	aligns[i] = pandoc.AlignLeft
			  elseif a_left == '-' and a_right == ':' then
              	aligns[i] = pandoc.AlignRight
			  elseif a_left == ':' and a_right == ':' then
              	aligns[i] = pandoc.AlignCenter
			  else
              	aligns[i] = pandoc.AlignDefault
			  end
              widths[i] = 0
            end
            return pandoc.utils.from_simple_table(
              pandoc.SimpleTable({}, aligns, widths, headrow, bodyrows))
          end ;
  TableHeader = Ct(V"BodyCell"^1)
              * cellsep
              * newline ;
  TableRow = Ct(V"BodyCell"^1)
             * cellsep
             * newline ;
  SeparatorRow = Ct(V"SeparatorCell"^1)
  			 * cellsep
			 * newline ;
  SeparatorCell = cellsep
             * spacechar^0
             * C(P(":")^-1 * P("-")^1 * P(":")^-1)
			 * spacechar^0
             / function(ils) return { pandoc.Plain(ils) } end ;
  HeaderCell = cellsep
             * spacechar^1
             * Ct((V"Inline" - (newline + cellsep))^0)
             / function(ils) return { pandoc.Plain(ils) } end ;
  BodyCell   = cellsep
             * spacechar^1
             * Ct((V"Inline" - (newline + cellsep))^0)
             / function(ils) return { pandoc.Plain(ils) } end ;
  RawBlock   = (P"\\newpage" + P"\\pagebreak")
             * newline
			 / function() 
				 return pandoc.RawBlock("latex", "\\newpage")
			 end ;
  Inline = V"Emph"
		 + V"Strong"
		 + V"LineBreak"
		 + V"Link"
		 + V"URL"
		 + V"Image"
		 + V"Math"
		 + V"Code"
		 + V"Superscript"
		 + V"Subscript"
		 + V"Str"
		 + V"Space"
		 + V"Special" ;
  Str = wordchar^1
      / pandoc.Str;
  Special = specialchar
          / pandoc.Str;
  Space = spacechar^1
        / pandoc.Space ;
  LineBreak = endline
            * # -(V"HorizontalRule" + V"CodeBlock")
            / pandoc.LineBreak ;
  Code = P"''"
	   * C((1 - P"''")^0)
	   * P"''"
	   / trim / pandoc.Code ;
  Link = P"[["
       * C((1 - (P"]]" + P"|"))^0)
       * (P"|" * Ct((V"Inline" - P"]]")^1))^-1
	   * P"]]"
       / function(url, desc)
           local txt = desc or {pandoc.Str(url)}
           return pandoc.Link(txt, url)
         end ;
  Image = P"{{"
        * #-P"{"
		* C((1 - (P"?" + P"}}"))^1) 
		* (S"?&" * P"height=" * C((1 - (P"&" + P"}}"))^1) + Cc(nil))
		* (S"?&" * P"href=" * C((1 - (P"&" + P"}}"))^1) + Cc(nil))
		* (S"?&" * P"id=" * C((1 - (P"&" + P"}}"))^1) + Cc(nil))
		* (S"?&" * P"width=" * C((1 - (P"}}"))^1) + Cc(nil))
        * P"}}"
        / function(url, height, href, id, width)
			text = id or ""
			local result = pandoc.Image(text, url, "fig:")
			result.attr = {height = height, width = width, href = href}
			result.attr.identifier = id
            return result
          end ;
  Math = P"$$"
       	 * C(1 - P"$$")
		 * P"$$"
		 / function(expression)
		 	return pandoc.Math(pandoc.DisplayMath, expression)
	 	 end ;
  Superscript = P"^{"
			  * Ct((V"Inline" -P"}")^1)
			  * P"}"
			  / pandoc.Superscript ;
  Subscript = P"_{"
			  * Ct((V"Inline" -P"}")^1)
			  * P"}"
			  / pandoc.Subscript ;
  URL = P"http"
      * P"s"^-1
      * P":"
      * (1 - (whitespacechar + (S",.?!:;\"'" * #whitespacechar)))^1
      / function(url)
          return pandoc.Link(pandoc.Str(url), url)
        end ;
  Emph = P"//"
       * Ct((V"Inline" - P"//")^1)
       * P"//"
       / pandoc.Emph ;
  Strong = P"**"
         * Ct((V"Inline" -P"**")^1)
         * P"**"
         / pandoc.Strong ;
  Meta = (P"Content-Type: text/x-zim-wiki" * newline)
		 * (P"Wiki-Format: zim " * C((1 - newline)^1) * newline)
		 * (P"Creation-Date: " * C((1 - newline)^1))^-1
		 * newline
		 / function(zim_version_string, creation_date_string)
      result_table = {}
      if zim_version_string == nil then
        error("The file is not a zim page. zim_version missing")
      end
      result_table["zim_version"] = pandoc.MetaString(zim_version_string)
      result_table["source_files"] = PANDOC_STATE.input_files
      if creation_date_string ~= nil then
        result_table["creation_date"] = pandoc.MetaString(creation_date_string)
      end
      return pandoc.Meta(result_table)
		 end ;
}

function Reader(input, reader_options)
  return lpeg.match(G, tostring(input))
end

