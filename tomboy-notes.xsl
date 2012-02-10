<?xml version='1.0' encoding="utf-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
xmlns:tomboy="http://beatniksoftware.com/tomboy"
xmlns:notes="http://beatniksoftware.com/tomboy/notes"
xmlns:size="http://beatniksoftware.com/tomboy/size"
xmlns:link="http://beatniksoftware.com/tomboy/link"
version='1.0'>

<xsl:output method="html" indent="no" />
<xsl:preserve-space elements="*" />

<xsl:param name="font" />
<xsl:param name="export-linked" />
<xsl:param name="export-linked-all" />
<xsl:param name="root-note" />

<xsl:param name="newline" select="'&#xA;'" />

<xsl:template match="/">
<html>
<head>
	<title>Tomboy Notes Export</title>
	<style type="text/css">/*<![CDATA[*/
		body { <xsl:value-of select="$font" /> }
		h1 { 
			font-size: xx-large;
			font-weight: bold;
			border-bottom: 1px solid black; 
		}
		div.note {
			position: relative;
			display: block;
			padding: 5pt;
			margin: 5pt;
			white-space: -moz-pre-wrap; /* Mozilla */
			white-space: -pre-wrap; /* Opera 4 - 6 */
			white-space: -o-pre-wrap; /* Opera 7 */
			white-space: pre-wrap; /* CSS3 */
			word-wrap: break-word; /* IE 5.5+ */ 
		}
		table.note-info{
			margin: 20px 0 5px;
			font-size:xx-small;
			border-width: 0 1px 1px 0;
			border-style: solid;
		}
		table.note-info td{
			padding: 2px 5px;
			border-width: 1px 0 0 1px;
			border-style: solid;
		}
		/*//]]>*/
	</style>
</head>
<body>
	<xsl:for-each select="notes/tomboy:note">
	<div class="note">
		<xsl:apply-templates select="tomboy:text | tomboy:title"/>

		<table class="note-info" boder="0" cellpadding="0" cellspacing="0"
			summary="Note Info">
			<tr>
				<td>Last updated:</td>	
				<td><xsl:value-of select="tomboy:last-change-date" /></td>
			</tr>	
			<tr>
				<td>Tags:</td>	
				<td>
					<xsl:for-each select="tomboy:tags">
					<div><xsl:value-of select="tomboy:tag"/></div>	
					</xsl:for-each>
				</td>
			</tr>	
		</table>
	</div>
	</xsl:for-each>
</body>
</html>
</xsl:template>

<!--<xsl:variable name="ignore-chars"><![CDATA["&#x1F;"]]></xsl:variable>-->


<xsl:template match="text()">
   <!--<xsl:value-of select="translate(., $ignore-chars, '')"/>-->
   <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="child::tomboy:text">
	<xsl:apply-templates select="node()"/>
</xsl:template>

<xsl:template match="tomboy:title">
	<h1 name="{node()}" id="{node()}"><xsl:value-of select="text()"/></h1>
</xsl:template>
<xsl:template match="tomboy:bold">
	<strong><xsl:apply-templates select="node()"/></strong>
</xsl:template>
<xsl:template match="tomboy:italic">
	<i><xsl:apply-templates select="node()"/></i>
</xsl:template>
<xsl:template match="tomboy:monospace">
	<code><xsl:apply-templates select="node()"/></code>
</xsl:template>

<xsl:template match="tomboy:strikethrough">
<strike><xsl:apply-templates select="node()"/></strike>
</xsl:template>

<xsl:template match="tomboy:highlight">
<span style="background:yellow"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="tomboy:datetime">
<span style="font-style:italic;font-size:small;color:#888A85">
<xsl:apply-templates select="node()"/>
</span>
</xsl:template>

<xsl:template match="size:small">
<span style="font-size:small"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="size:large">
<span style="font-size:large"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="size:huge">
<span style="font-size:xx-large"><xsl:apply-templates select="node()"/></span>
</xsl:template>

<xsl:template match="link:broken">
<span style="color:#555753;text-decoration:underline">
<xsl:value-of select="node()"/>
</span>
</xsl:template>
<xsl:template match="link:internal">
<a style="color:#204A87" href="#{node()}">
<xsl:value-of select="node()"/>
</a>
</xsl:template>

<xsl:template match="link:url">
	<xsl:choose>
		<xsl:when test="contains(node(), '@')">
			<a style="color:#3465A4" href="mailto:{node()}"><xsl:value-of select="node()"/></a>
		</xsl:when>
		<xsl:otherwise>
			<a style="color:#3465A4" href="{node()}"><xsl:value-of select="node()"/></a>
		</xsl:otherwise>
	</xsl:choose>

</xsl:template>

<xsl:template match="tomboy:list">
<ul>
<xsl:apply-templates select="tomboy:list-item" />
</ul>
</xsl:template>

<xsl:template match="tomboy:list-item">
<li>
<xsl:if test="normalize-space(text()) = ''">
<xsl:attribute name="style">list-style-type: none</xsl:attribute>
</xsl:if>
<xsl:attribute name="dir">
<xsl:value-of select="@dir"/>
</xsl:attribute>
<xsl:apply-templates select="node()" />
</li>
</xsl:template>

<xsl:template match="//tomboy:x | //tomboy:y | //tomboy:width | //tomboy:height | //tomboy:cursor-position | //tomboy:create-date | tomboy:last-change-date | tomboy:open-on-startup | tomboy:last-metadata-change-date | tomboy:tags">
<xsl:comment>literal</xsl:comment>
</xsl:template>

</xsl:stylesheet>
