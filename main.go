package main

import (
	"os/exec"

	"io"
	"os"
	"strings"
)

func containAnyOf(text string, list []string) bool {
	for _, v := range list {
		if strings.Contains(text, v) {
			return true
		}
	}
	return false
}

func addDiv(text string) string {
	var result string
	bool := false
	listByLine := strings.Split(text, "\n")

	for i := 0; i < len(listByLine)-1; i++ {
		line := listByLine[i]

		if strings.Contains(line, "**") {
			if !containAnyOf(listByLine[i+1], []string{"**", "#", "##", "###"}) {
				result += "\n<div style=\"page-break-inside: avoid;\">\n"
				bool = true
			}
		}

		if len(line) < 1 {
			if containAnyOf(listByLine[i+1], []string{"**", "#", "##", "###"}) {

				if bool {
					result += "\n</div>\n"
					bool = false
				}
			}
		}
		result += "\n" + line
	}

	result += listByLine[len(listByLine)-1]
	return result
}

func main() {
	fi, err := os.Open("school.md")
	if err != nil {
		panic(err)
	}

	defer func() {
		if err := fi.Close(); err != nil {
			panic(err)
		}
	}()

	content, err := io.ReadAll(fi)
	text := addDiv(string(content))
	tmpMdFile := "temp.md"
	if err := os.WriteFile(tmpMdFile, []byte(text), 0666); err != nil {
		panic(err)
	}

	outputFile := "school.html"
	cmd := exec.Command("pandoc", tmpMdFile, "-o", outputFile, "--template=template.html")
	if err := cmd.Run(); err != nil {
		panic(err)
	}

	if err := os.Remove(tmpMdFile); err != nil {
		panic(err)
	}

	println("done")

}
