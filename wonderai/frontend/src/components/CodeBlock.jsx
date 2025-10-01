import React, { useState, useCallback } from 'react'
import { MagicButton, MagicBadge, MagicTooltip } from '@/components/magicui'
import {
    Copy,
    Check,
    Code2,
    Download,
    Play
} from 'lucide-react'
import { toast } from 'sonner'
import { cn } from '@/lib/utils'

/**
 * CodeBlock component with syntax highlighting and copy functionality
 * Provides a rich code viewing experience with language detection and actions
 */
export const CodeBlock = React.memo(({
    children,
    className = '',
    language = 'text',
    showLineNumbers = true,
    allowCopy = true,
    allowDownload = true,
    filename = null,
    ...props
}) => {
    const [copied, setCopied] = useState(false)
    const [isExecuting, setIsExecuting] = useState(false)

    // Extract code content from children
    const codeContent = React.useMemo(() => {
        if (typeof children === 'string') return children
        if (React.isValidElement(children) && children.props.children) {
            return children.props.children
        }
        return String(children || '')
    }, [children])

    // Handle copy to clipboard
    const handleCopy = useCallback(async () => {
        try {
            await navigator.clipboard.writeText(codeContent)
            setCopied(true)
            toast.success('Code copied to clipboard')

            // Reset copied state after 2 seconds
            setTimeout(() => setCopied(false), 2000)
        } catch {
            toast.error('Failed to copy code')
        }
    }, [codeContent])

    // Handle download as file
    const handleDownload = useCallback(() => {
        const fileExtension = getFileExtension(language)
        const fileName = filename || `code-snippet.${fileExtension}`

        const blob = new Blob([codeContent], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)

        const link = document.createElement('a')
        link.href = url
        link.download = fileName
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        URL.revokeObjectURL(url)
        toast.success(`Downloaded ${fileName}`)
    }, [codeContent, language, filename])

    // Handle code execution (placeholder for future implementation)
    const handleExecute = useCallback(async () => {
        if (!isExecutableLanguage(language)) return

        setIsExecuting(true)
        toast.info('Code execution feature coming soon!')

        // Simulate execution delay
        setTimeout(() => {
            setIsExecuting(false)
        }, 1000)
    }, [language])

    // Split code into lines for line numbers
    const codeLines = React.useMemo(() => {
        return codeContent.split('\n')
    }, [codeContent])

    // Get language display name
    const displayLanguage = getLanguageDisplayName(language)

    return (
        <div className="group relative">
            {/* Header with language and actions */}
            <div className="flex items-center justify-between px-4 py-2 bg-muted/50 border border-b-0 rounded-t-lg">
                <div className="flex items-center gap-2">
                    <Code2 className="w-4 h-4 text-muted-foreground" />
                    <MagicBadge variant="secondary" className="text-xs">
                        {displayLanguage}
                    </MagicBadge>
                    {filename && (
                        <span className="text-sm text-muted-foreground font-mono">
                            {filename}
                        </span>
                    )}
                </div>

                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    {allowCopy && (
                        <MagicTooltip content="Copy code">
                            <MagicButton
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7"
                                onClick={handleCopy}
                            >
                                {copied ? (
                                    <Check className="w-3 h-3 text-green-500" />
                                ) : (
                                    <Copy className="w-3 h-3" />
                                )}
                            </MagicButton>
                        </MagicTooltip>
                    )}

                    {allowDownload && (
                        <MagicTooltip content="Download as file">
                            <MagicButton
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7"
                                onClick={handleDownload}
                            >
                                <Download className="w-3 h-3" />
                            </MagicButton>
                        </MagicTooltip>
                    )}

                    {isExecutableLanguage(language) && (
                        <MagicTooltip content="Execute code">
                            <MagicButton
                                variant="ghost"
                                size="icon"
                                className="h-7 w-7"
                                onClick={handleExecute}
                                disabled={isExecuting}
                            >
                                <Play className={cn(
                                    "w-3 h-3",
                                    isExecuting && "animate-spin"
                                )} />
                            </MagicButton>
                        </MagicTooltip>
                    )}
                </div>
            </div>

            {/* Code content */}
            <div className="relative">
                <pre className={cn(
                    "overflow-x-auto p-4 bg-card border border-t-0 rounded-b-lg",
                    "text-sm font-mono leading-relaxed",
                    className
                )} {...props}>
                    <code className={`language-${language}`}>
                        {showLineNumbers ? (
                            <div className="flex">
                                {/* Line numbers */}
                                <div className="select-none pr-4 text-muted-foreground/60 border-r border-border/50 mr-4">
                                    {codeLines.map((_, index) => (
                                        <div key={index} className="text-right">
                                            {index + 1}
                                        </div>
                                    ))}
                                </div>

                                {/* Code content */}
                                <div className="flex-1">
                                    {codeLines.map((line, index) => (
                                        <div key={index} className="min-h-[1.5rem]">
                                            {line || '\u00A0'} {/* Non-breaking space for empty lines */}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            codeContent
                        )}
                    </code>
                </pre>

                {/* Copy overlay for quick access */}
                {allowCopy && (
                    <Button
                        variant="ghost"
                        size="icon"
                        className={cn(
                            "absolute top-2 right-2 h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity",
                            "bg-background/80 backdrop-blur-sm border"
                        )}
                        onClick={handleCopy}
                        title="Copy code"
                    >
                        {copied ? (
                            <Check className="w-4 h-4 text-green-500" />
                        ) : (
                            <Copy className="w-4 h-4" />
                        )}
                    </Button>
                )}
            </div>
        </div>
    )
})

CodeBlock.displayName = 'CodeBlock'

// Helper functions
function getFileExtension(language) {
    const extensions = {
        javascript: 'js',
        typescript: 'ts',
        python: 'py',
        java: 'java',
        cpp: 'cpp',
        c: 'c',
        csharp: 'cs',
        go: 'go',
        rust: 'rs',
        php: 'php',
        ruby: 'rb',
        swift: 'swift',
        kotlin: 'kt',
        scala: 'scala',
        html: 'html',
        css: 'css',
        scss: 'scss',
        sass: 'sass',
        less: 'less',
        json: 'json',
        xml: 'xml',
        yaml: 'yml',
        markdown: 'md',
        bash: 'sh',
        shell: 'sh',
        sql: 'sql',
        docker: 'dockerfile',
        dockerfile: 'dockerfile',
    }

    return extensions[language.toLowerCase()] || 'txt'
}

function getLanguageDisplayName(language) {
    const displayNames = {
        javascript: 'JavaScript',
        typescript: 'TypeScript',
        python: 'Python',
        java: 'Java',
        cpp: 'C++',
        c: 'C',
        csharp: 'C#',
        go: 'Go',
        rust: 'Rust',
        php: 'PHP',
        ruby: 'Ruby',
        swift: 'Swift',
        kotlin: 'Kotlin',
        scala: 'Scala',
        html: 'HTML',
        css: 'CSS',
        scss: 'SCSS',
        sass: 'Sass',
        less: 'Less',
        json: 'JSON',
        xml: 'XML',
        yaml: 'YAML',
        markdown: 'Markdown',
        bash: 'Bash',
        shell: 'Shell',
        sql: 'SQL',
        docker: 'Docker',
        dockerfile: 'Dockerfile',
    }

    return displayNames[language.toLowerCase()] || language.toUpperCase()
}

function isExecutableLanguage(language) {
    const executableLanguages = [
        'javascript', 'python', 'bash', 'shell', 'sql'
    ]

    return executableLanguages.includes(language.toLowerCase())
}

export default CodeBlock
