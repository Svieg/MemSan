#ifndef LOG6302_VISITOR_H
#define LOG6302_VISITOR_H

#include <iostream>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/AST/ASTContext.h>
#include <clang/Lex/Lexer.h>
#include <clang/Frontend/CompilerInstance.h>

/**
 * LOG6302 Cette classe est un exemple d'un visiteur récursif de clang. À l'intérieur, vous pouvez y trouver deux exemples
 * de visites, et un exemple de traverse.
 */
class Visitor : public clang::RecursiveASTVisitor<Visitor> {
public:

  Visitor(clang::ASTContext &context) : context_(context) {};

  // Visites
  bool VisitCXXRecordDecl(clang::CXXRecordDecl *D);
  bool VisitIfStmt(clang::IfStmt *S);

  // Traverses
  bool TraverseCXXMethodDecl(clang::CXXMethodDecl *D);

private:
  clang::ASTContext &context_;


  std::string GetStatementString(clang::Stmt *S) {
    bool invalid;
    if (!S) return "Something";

    clang::CharSourceRange conditionRange = clang::CharSourceRange::getTokenRange(S->getLocStart(), S->getLocEnd());
    std::string str = clang::Lexer::getSourceText(conditionRange, context_.getSourceManager(), context_.getLangOpts(), &invalid);
    if (invalid)
      return "Something";
    encode(str);
    return str;
  }

  void encode(std::string& data) {
    std::string buffer;
    buffer.reserve(data.size());
    for(size_t pos = 0; pos != data.size(); ++pos) {
      switch(data[pos]) {
        case '&':  buffer.append("&amp;");       break;
        case '\"': buffer.append("&quot;");      break;
        case '\'': buffer.append("&apos;");      break;
        case '<':  buffer.append("&lt;");        break;
        case '>':  buffer.append("&gt;");        break;
        case '\n':  buffer.append("\\n");        break;
        case '\\':  buffer.append("\\\\");        break;
        case '|':  buffer.append("\\|");        break;
        default:   buffer.append(&data[pos], 1); break;
      }
    }
    data.swap(buffer);
  }
};


#endif //LOG6302_VISITOR_H
