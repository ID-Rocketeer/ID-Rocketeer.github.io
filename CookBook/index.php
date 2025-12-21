<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <title>The Collins Family Cookbook</title>
    <link rel="stylesheet" type="text/css" href="style/index.css" title="index style"/>
    <link rel="icon" type="image/png" href="images/favicon.png"/>
  </head>
  <body>
    <h1>Collins<br/>Cookbook</h1>

<?php
  error_reporting(E_ALL);

  /**
   * This class processes sub-directories contained in the "recipe" sub-directory of the current working directory.
   * Each sub-directory of the "recipe" directory is assumed to name a different catagory of recipes. 
   * (i.e. Desserts, Drinks, etc.) The assumption is that the each category directory contains valid Recipe language
   * (an XML language) files representing recipes appropriate to that category. The indexer extracts the contents of
   * the "title" element of each file for presentation in the cook book index.
   * @author Steven P. Collins
   * @copyright 2005 Steven P. Collins
   */
  class CategoryIndexer {
    var $tagname;			// used to track XML tags while parsing
    var $recipetitle;			// stores the title of the recipe when found during XML parsing
    var $recipes = array();		// stores the list of recipe URIs keyed by title as they are parsed out of the XML files

    /**
     * Callback function for the xml_parse method invoked for each start tag encountered. Has the side effect
     * of preserving the most recent encountered tag in the tagname member variable. When the tagname is "title" the
     * recipetitle member variable is also cleared.
     * 
     * @param resource $parser the instance of xml_parser invoking this callback method.
     * @param string $name then name of the start tag encountered by the parser.
     * @param array $attribs the attribute name value pairs stored in an associative array.
     */
    function startElement ($parser, $name, $attribs) {
      $this->tagname = $name;

      if ($this->tagname == 'title') {
        $this->recipetitle = "";
      }
    }
 
    /**
     * Callback function for the xml_parse method provided for completeness.
     * 
     * @param resource $parser the instance of xml_parser invoking this callback method.
     * @param string $name the name of the end tag encountered by the parser.
     */
    function endElement ($parser, $name) {
      // do nothing, provided to avoid warning with all errors turned on.
    }
 
    /**
     * Callback function for the xml_parse method invoked for all text located between tags. Accumulates the recipe
     * title found between the <title> and </title> tags in the recipetitle member variable.
     * 
     * @param resource $parser the instance of xml_parser invoking this callback method.
     * @param string $cdata the character data detected between tags.
     */ 
    function charHandler ($parser, $cdata) {
      if ($this->tagname == 'title') {
        $this->recipetitle .= $cdata;
      }
    }

	/**
	 * Converts a path to a URI. Most significant is the conversion of spaces to %20.
	 * 
	 * @param string $path the relative path to be converted to a URI.
	 * 
	 * @return string the URI form of the passed in $path
	 */
	function makeURI ($path) {
	  // Break the string apart on the "/" path seperators.
	  $components = explode("/", $path);

	  // Run each component through the rawurlencode() method.
	  foreach($components as $key => $component) {
	  	$components[$key] = rawurlencode($component);
	  }

	  // Recombine the components with the "/" path seperator.
	  $uri = implode("/", $components);
	  return $uri;
	}

    /**
     * Runs the XML parser over the named recipefile to extract the title.
     * 
     * @param string $recipefile the path to the recipe file starting with the "recipes" directory.
     * @param integer $key the ordinal location of the array of recipes.
     */
    function extractRecipeTitle ($recipefile, $key) {

      // establish a new parser to use for this file
      $parser = xml_parser_create_ns();

      // ensure the data doesn't get mangled.
      xml_parser_set_option ($parser, XML_OPTION_CASE_FOLDING, FALSE);

      // prepare the parser for use in an object.
      xml_set_object($parser, $this);

      // set the handlers so we can recognize tags and character data in the file.
      xml_set_element_handler ($parser, "startElement", "endElement");
      xml_set_character_data_handler ($parser, "charHandler");

      // load the entire contents of the recipe file for parsing
      $recipeXML = file_get_contents ($recipefile);
      
      // process the recipe through the parser
      xml_parse ($parser, $recipeXML, false);
      
      // clean up
      xml_parser_free ($parser);
      
      // add the URI for the recipe to the array of recipes keyed by the title
      $this->recipes[trim($this->recipetitle)] = $this->makeURI($recipefile);
    }

    /**
     * Performs XML parsing of each file in the named directory to extract the recipe titlea.
     *
     * @param string $dirname the name of a directory representing a particular catagory of recipes.
     * @return array of relative recipe URIs keyed and sorted by recipe title.
     */
    function processCategory ($dirname) {
      echo "<!-- processCategory (" . $dirname . ") -->\n";
      $recipefiles = glob($dirname . "/*.xml");

      if ($recipefiles) { // Make sure we found at least one XML file to process
        // Construct the array for the callback as shown rather than using "array($this, 'extractRecipeTitle')" so it will
        // contain a reference to the current object, rather than a copy of the current object.
      	$callback[0] = &$this;
      	$callback[1] = 'extractRecipeTitle';
        array_walk ($recipefiles, $callback);
      }

      ksort ($this->recipes);
      return $this->recipes;
    }
  }

  /**
   * Outputs an HTML list item for the recipe defined by the passed in recipefile and recipetitle.
   * 
   * @param string $recipefile the relative URI to the recipe on the server.
   * @param string $recipetitle the ttile to be displayed in the index for the recipe
   */
  function printIndexEntry ($recipefile, $recipetitle) {
    echo "          <li><a href=" . '"' . $recipefile . '">' . trim ($recipetitle) . "</a></li>\n";
  }

  /**
   * Outputs the category description and then generates the unordered list for all of the XML files contained
   * in the directory named by the filename parameter.
   * 
   * @param string $filename the name of "catagory" directory containing recipes.
   * @param integer $key the associate key in the array containing the recipes catagory names.
   */
  function indexCategory ($filename, $key, $indexer) {
    echo "<!-- indexCategory: ". $filename ." " . $key . " " . " -->\n";
    $indexer->recipes = array();
    echo "<!-- is_dir (" . $filename . ") : " .  (is_dir($filename) ? "true" : "false") . " -->\n";

    if (is_dir($filename)) {
      $indexEntries = $indexer->processCategory ($filename);

      if (0 < count($indexEntries)) {
        echo "      <li>\n        <h2>" . basename($filename) . "</h2>\n        <ul>\n";
        array_walk ($indexEntries, 'printIndexEntry');
        echo "        </ul>\n        <br/>\n";
        echo "      </li>\n";
      }
    }
  }

  // Here it is, the main body of the program! Walks through the contents of the recipes directory.
  echo "    <!-- Index produced on " . strftime("%c") . " -->\n\n";
  echo "    <ul>";
  array_walk (glob("recipes/*"), 'indexCategory', new CategoryIndexer ());
  echo "    </ul>";
?>

  </body>
</html>
