#include "Visitor.h"

/**********************/
/* C++ Class traverse */
/**********************/
bool Visitor::VisitCXXRecordDecl(clang::CXXRecordDecl *D) {
  std::cout<<"[LOG6302] Visite de la classe \""<<D->getName().str()<<"\"\n";
  return true;
}

/**********************/
/* If visit           */
/**********************/

bool Visitor::VisitIfStmt(clang::IfStmt *S) {
  std::cout<<"[LOG6302] Visite d'une condition : \" if ("<<GetStatementString(S->getCond())<<") \"\n";
  return true;
}

/***********************/
/* C++ Method traverse */
/***********************/
bool Visitor::TraverseCXXMethodDecl(clang::CXXMethodDecl *D) {

  if (!D->isThisDeclarationADefinition()) {
    return true;
  }

  clang::FullSourceLoc location = context_.getFullLoc(D->getLocStart());

  std::string  file_path   = context_.getSourceManager().getFileEntryForID(location.getFileID())->getName();
  unsigned int line_number = location.getSpellingLineNumber();

  std::cout
    <<"[LOG6302] Traverse de la méthode \""
    <<D->getName().str()
    <<"\" ("
    << file_path
    << ":"
    <<line_number
    <<")\n";

  clang::RecursiveASTVisitor<Visitor>::TraverseCXXMethodDecl(D);

  std::cout<<"[LOG6302] Fin traverse de la méthode \""<<D->getName().str()<<"\"\n";

  return true;
}